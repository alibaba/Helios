为了防止在反序列化漏洞，在使用Hessian进行反序列化时，应该创建`WhiteListSerializerFactory类实现SerializerFactory#loadSerializedClass`进行白名单限制，并通过`Hessian2Input#setSerializerFactory`设置该`factory`。下面为示例代码。

```java
public class WhiteListSerializerFactory extends SerializerFactory {

    private static final List<String> WHITELIST_CLASS_SET = new ArrayList<String>();

    static {
        // 下方添加允许的反序列化目标类， 以及其Field相关的类
        WHITELIST_CLASS_SET.add("com.example.class");
    }

    /**
     * 检查类名是否在白名单中
     * @param className 类名
     * @return 是否允许
     */
    private boolean isAllowed(String className) {
        if (className == null || className.isEmpty()) {
            return false;
        }
        
        // 直接匹配
        if (WHITELIST_CLASS_SET.contains(className)) {
            return true;
        }
        
        return false;
    }

 
    @Override
    public Class<?> loadSerializedClass(String className) throws ClassNotFoundException {
        if (!isAllowed(className)) {
            throw new SecurityException(
                    "Unauthorized Hessian deserialization attempt for class: " + className
            );
        }
        return super.loadSerializedClass(className);
    }
}
```

注意不要将下面的类加入到白名单中
1. java.lang.Object
