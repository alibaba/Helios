在使用Apache HttpClient4发起HTTP请求时，为防止出现SSRF漏洞应
1. 实现SsrfBlockerDnsResolver类重载DnsResolver#resolve方法，对解析后的address进行检查，判断是否为内网地址
2. 基于SsrfBlockerDnsResolver创建PoolingHttpClientConnectionManager
3. 在创建HttpClient的时候调用setConnectionManager传入第二步创建的manager

可以参考下面的代码实现上述逻辑，但是要注意下面的代码未出现在当前目录中，只是演示代码
```java
import java.net.InetAddress;
import java.net.UnknownHostException;

import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.config.RegistryBuilder;
import org.apache.http.conn.DnsResolver;
import org.apache.http.conn.socket.ConnectionSocketFactory;
import org.apache.http.conn.socket.PlainConnectionSocketFactory;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.impl.conn.PoolingHttpClientConnectionManager;
import org.apache.http.impl.conn.SystemDefaultDnsResolver;

public class JsonFetcherWithHttpClient4 implements JsonFetcher {
    @Override
    public String fetchJson(String url) throws Exception {
        try (CloseableHttpClient client = createSecureHttpClient()) {
            HttpGet request = new HttpGet(url);
            try (CloseableHttpResponse response = client.execute(request)) {
                //
            }
        }
    }

    /**
     * 创建一个配置了自定义 DnsResolver 的 HttpClient 以防止 SSRF。
     * @return 配置好的 CloseableHttpClient 实例
     */
    private static CloseableHttpClient createSecureHttpClient() {
        // 创建一个连接管理器，并为其提供我们的安全 DNS 解析器
        PoolingHttpClientConnectionManager connManager = new PoolingHttpClientConnectionManager(
            // 注册 http 和 https 协议的 Socket 工厂
            RegistryBuilder.<ConnectionSocketFactory>create()
                .register("http", PlainConnectionSocketFactory.getSocketFactory())
                .register("https", SSLConnectionSocketFactory.getSocketFactory())
                .build(),
            null, // Connection factory
            new SsrfBlockerDnsResolver() // 关键：在这里注入我们的 DNS 解析器
        );

        // 使用自定义的连接管理器来构建 HttpClient
        return HttpClients.custom()
                .setConnectionManager(connManager)
                .build();
    }

    /**
     * 一个自定义的 DnsResolver，用于在解析域名时检查 IP 地址，阻止对私有网络的访问。
     */
    static class SsrfBlockerDnsResolver implements DnsResolver {

        // 使用默认的系统 DNS 解析器来实际执行解析
        private final DnsResolver systemResolver = SystemDefaultDnsResolver.INSTANCE;

        @Override
        public InetAddress[] resolve(String host) throws UnknownHostException {
            // 首先，使用系统默认解析器获取所有 IP 地址
            InetAddress[] addresses = systemResolver.resolve(host);

            // 检查每一个解析出的 IP 地址
            for (InetAddress address : addresses) {
                if (isPrivate(address)) {
                    // 如果发现任何一个地址是私有或本地地址，就抛出异常。
                    // UnknownHostException 在语义上是合适的，因为它阻止了到该主机的“可知”连接。
                    throw new UnknownHostException("SSRF attempt detected: resolution of host '" + host + "' to a private address " + address + " is blocked.");
                }
            }

            // 如果所有地址都通过了检查，则正常返回
            return addresses;
        }

        /**
         * 检查一个 InetAddress 是否是私有地址、回环地址或本地链接地址。
         * @param address 要检查的地址
         * @return 如果是私有地址则返回 true
         */
        private boolean isPrivateIP(InetAddress address) {
            return address.isSiteLocalAddress() || // 10.x.x.x, 172.16.x.x ~ 172.31.x.x, 192.168.x.x
                    address.isLoopbackAddress() ||  // 127.x.x.x
                    address.isAnyLocalAddress() || // 0.0.0.0
                    address.isLinkLocalAddress();   // 169.254.x.x
        }
    }
}
```