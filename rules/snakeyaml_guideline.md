为了防止snakeyaml 1.x版本在反序列化用户传入的yaml的时候出现反序列化漏洞，应该
1. 如果知道对应的类型可以使用`loadAs(yamlContent, SomeClass.class)`
2. 否则在创建yaml的时候应通过`new Yaml(SafeConstructor())`