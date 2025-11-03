为了防止出现SPEL表达式注入漏洞，应使用
```java
SimpleEvaluationContext context = SimpleEvaluationContext.forReadOnlyDataBinding().build();
```
如果需要执行`"".length()`等方法调用，可以使用
```java
SimpleEvaluationContext context = SimpleEvaluationContext.forReadOnlyDataBinding().withMethodResolvers(DataBindingMethodResolver.forInstanceMethodInvocation()).build();
```