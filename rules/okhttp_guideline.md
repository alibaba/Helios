在使用okhttp发起HTTP请求时，为防止出现SSRF漏洞应
1. 实现SsrfEventBlocker类重载EventListener#connectStart方法，对inetSocketAddress进行检查，判断是否为内网地址
2. 基于SsrfEventBlocker创建EventListener.Factory
3. 在创建OkHttpClient的时候调用eventListenerFactory传入第二步创建的factory

可以参考下面的代码实现上述逻辑，但是要注意下面的代码未出现在当前目录中，只是演示代码
```java
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Proxy;

import okhttp3.Call;
import okhttp3.EventListener;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class JsonFetcherWithOkHttp implements JsonFetcher {
    @Override
    public String fetchJson(String url) throws Exception {
        OkHttpClient client = createSecureHttpClient();
        
        Request request = new Request.Builder().url(url).build();
        try (Response response = client.newCall(request).execute()) {
            return response.body() != null ? response.body().string() : null;
        }
    }

    private static OkHttpClient createSecureHttpClient() {
        // EventListener.Factory 确保每个 Call 都有一个新的 EventListener 实例，
        // 这对于并发请求是安全的。
        EventListener.Factory factory = call -> new SsrfEventBlocker();

        return new OkHttpClient.Builder()
                .eventListenerFactory(factory)
                .build();
    }

    static class SsrfEventBlocker extends EventListener {
        @Override
        public void connectStart(Call call, InetSocketAddress inetSocketAddress, Proxy proxy) {
            InetAddress address = inetSocketAddress.getAddress();
            if (isPrivate(address)) {
                // 如果是私有或本地地址，则抛出异常，阻止连接。
                throw new SecurityException("SSRF attempt detected: connection to " + address + " is blocked.");
            }
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