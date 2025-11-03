在将用户输入拼接至HTML中为防止出现XSS应
1. 在渲染富文本时，不能直接HTML编码，为防止出现XSS应
    1.设置CSP来防止XSS攻击，CSP的script-src需要同时带有'nonce-xxx' 'Strict-Dynamic'两个字段，即使用nonce-based CSP
    ```
    ```
    或者
    2.使用白名单方式过滤html标签及属性值来防止XSS攻击
    可参考代码
    ```java
    /**
     * 创建安全的HTML标签白名单
     */
    private Safelist createSafelist() {
        return Safelist.relaxed()
                .addTags("strike", "s", "u")
                // 对img标签进行更严格的控制
                .addAttributes("img", "alt", "width", "height", "src")
                // 只允许安全的协议
                .addProtocols("img", "src", "https")
                // 移除可能造成安全问题的属性
                .removeAttributes("img", "onclick", "onerror", "onload");
    }
    ```
2. 在渲染普通文本时，可直接进行HTML编码，然后再拼接至HTML中，以防止出现XSS漏洞。