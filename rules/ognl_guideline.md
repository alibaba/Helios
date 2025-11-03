为了防止执行Ognl表达式时出现安全漏洞，应实现AbstractMemberAccess，重载isAccessible方法，对member的class进行白名单校验，目前已经内置了一些基础类型，还需要根据业务逻辑，添加业务白名单类。
可参考下面的代码实现上述的流程，注意目前目录中并不存在SecurityMemberAccess，如需使用需要以static class包含在代码中
```java
import ognl.AbstractMemberAccess;
import ognl.OgnlContext;

import java.lang.reflect.Member;
import java.util.List;
import java.util.Set;
import java.util.HashSet;
import java.util.Arrays;

public class SecurityMemberAccess extends AbstractMemberAccess {
    Set<String> allowClassSet = new HashSet<>();

    //请注意，设置自定义白名单包名时切勿将当前工具类的包名放入
    private static final List<String> defaultAllowClasses= Arrays.asList(

            // 基础类型
            "java.lang.String",
            "java.lang.Integer",
            "java.lang.Long",
            "java.lang.Double",
            "java.lang.Boolean",
            "java.lang.Object",
            "java.math.BigDecimal",

            // 日期时间类
            "java.util.Date",
            "java.sql.Date",
            "java.time.LocalDateTime",
            "java.time.LocalDate",

            // 集合类
            "java.util.List",
            "java.util.ArrayList",
            "java.util.Map",
            "java.util.HashMap",
            "java.util.Set",
            "java.util.HashSet"
            // 添加用到了业务类
    );

    public SecurityMemberAccess() {
        this.allowClassSet.addAll(defaultAllowClasses);
    }

    public SecurityMemberAccess(List<String> allowClasses){
        this.allowClassSet.addAll(allowClasses);
    }


    @Override
    public boolean isAccessible(OgnlContext context, Object o, Member member, String s) {
        //取出当前调用方法的类名
        String className = member.getDeclaringClass().getName();

        // 判断是否在白名单内
        for (String allowedPackage : allowClassSet) {
            if (className.startsWith(allowedPackage)) {
                return true;
            }
        }
        //默认不通过 强检测
        return false;
    }
}
```
使用示例
```java
OgnlContext context = new OgnlContext(new DefaultClassResolver(), new DefaultTypeConverter(), new SecurityCustomMemberAccess());
Object result = Ognl.getValue(expression, context, user);
```
当ognl的版本小于3.4.0时，`public boolean isAccessible(OgnlContext context, Object o, Member member, String s)`的签名为`public boolean isAccessible(Map context, Object o, Member member, String s)`，这时需要将`OgnlContext`对象转换成`Map`对象