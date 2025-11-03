为了防止出现SSRF漏洞，应
1. 检查输入URL对应HOST的IP是否为内网IP,可使用下面的函数判断是否为内网IP
   ```java
    /**
     * 判断 host 是否是内网 IP（支持域名或 IP 字符串）
     */
    public boolean isPrivateIP(String host) {
            try {
                InetAddress address = InetAddress.getByName(host);
                return isPrivateIP(address);
            } catch (UnknownHostException e) {
                // 主机名无法解析，返回 false 或抛异常根据需求处理
                return false;
            }
    }
   /**
         * 检查一个 InetAddress 是否是私有地址、回环地址或本地链接地址。
         * @param address 要检查的地址
         * @return 如果是私有地址则返回 true
         */
    public boolean isPrivateIP(InetAddress address) {
        return address.isSiteLocalAddress() || // 10.x.x.x, 172.16.x.x ~ 172.31.x.x, 192.168.x.x
                address.isLoopbackAddress() ||  // 127.x.x.x
                address.isAnyLocalAddress() || // 0.0.0.0
                address.isLinkLocalAddress();   // 169.254.x.x
    }
   ```
2. 禁止302跳转