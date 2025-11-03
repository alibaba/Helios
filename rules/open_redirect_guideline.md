在进行重定向时，应检查重定向对应的HOST是否在白名单中，以防止出现任意重定向漏洞。可参考下面的代码实现。
```java
/**
* 检查URL是否在允许的域名列表中
* @param url 待检查的URL
* @return 如果URL被允许返回true，否则返回false
*/
private boolean isUrlAllowed(String url) {
    try {
        URI uri = new URI(url);
        String host = uri.getHost();
        
        // 如果没有主机名（可能是相对路径），则允许
        if (host == null || host.isEmpty()) {
            return true;
        }
        
        // 检查主机名是否在白名单中
        return ALLOWED_HOSTS.contains(host);
    } catch (URISyntaxException e) {
        // 如果URL格式不正确，拒绝重定向
        return false;
    }
}
```