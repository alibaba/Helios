在使用xmldecoder反序列化不可信的xml时，应传入自定义白名单的ClassLoader以防止出现反序列化漏洞。
```
class WhiteListClassLoader extends ClassLoader {
        private final Set<String> whiteList;
        
        public WhiteListClassLoader(ClassLoader parent, Set<String> whiteList) {
            super(parent);
            this.whiteList = whiteList;
        }
        
        @Override
        protected Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {
            if (whiteList.contains(name)) {
                return super.loadClass(name, resolve);
            } else {
                // 一定要抛RuntimeException否则会被Catch
                throw new RuntimeException("Class not allowed: " + name);
            }
        }
    }
```