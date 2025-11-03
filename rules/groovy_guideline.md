为了防止执行Groovy脚本时出现安全漏洞，应按照下面三个步骤进行配置
1. 创建WhiteListSecureASTCustomizer进行安全增强可参考下面的代码实现上述的流程，注意目前目录中并不存在WhiteListSecureASTCustomizer，如需使用需要以static class包含在代码中
```java
import org.codehaus.groovy.ast.ClassNode;
import org.codehaus.groovy.ast.expr.ConstructorCallExpression;
import org.codehaus.groovy.ast.expr.Expression;
import org.codehaus.groovy.ast.expr.MethodCallExpression;
import org.codehaus.groovy.ast.expr.StaticMethodCallExpression;
import org.codehaus.groovy.control.customizers.SecureASTCustomizer;

import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;


public class WhiteListSecureASTCustomizer extends SecureASTCustomizer {
    private static final List<String> defaultReceiverWhiteList = Arrays.asList(
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
            "java.util.HashSet",

            //工具类
            "java.lang.Math"
    );
    public WhiteListSecureASTCustomizer(){
        this(defaultReceiverWhiteList);
    }

    public WhiteListSecureASTCustomizer(List<String> receiverWhiteList){
        this.setClosuresAllowed(false);
        this.setReceiversWhiteList(receiverWhiteList);
        Set<String> whiteListMethod = getWhiteListMethod(receiverWhiteList);

        this.addExpressionCheckers(expr -> {
            String fullMethodName = "";
            if (expr instanceof MethodCallExpression) {
                MethodCallExpression methodCall = (MethodCallExpression) expr;
                Expression objectExpr = methodCall.getObjectExpression();
                ClassNode type = objectExpr.getType();
                String typeName = type.getName();
                String methodName = methodCall.getMethodAsString();//获取方法名
                fullMethodName = String.format("%s#%s", typeName, methodName);
            }else if (expr instanceof StaticMethodCallExpression){
                StaticMethodCallExpression methodCall = (StaticMethodCallExpression) expr;
                ClassNode type = methodCall.getOwnerType();
                String typeName = type.getName();
                String methodName = methodCall.getMethodAsString();
                fullMethodName = String.format("%s#%s", typeName, methodName);
            }else if (expr instanceof ConstructorCallExpression){
                ConstructorCallExpression constructorCall = (ConstructorCallExpression) expr;
                ClassNode type = constructorCall.getType();
                String typeName = type.getName();
                String methodName = constructorCall.getMethodAsString();
                fullMethodName = String.format("%s#%s", typeName, methodName);
            }

            if (!fullMethodName.isEmpty() && !whiteListMethod.contains(fullMethodName)){
                throw new SecurityException("Calling " + fullMethodName + " is not allowed");
            }
            return true;
        });
    }

    public Set<String> getWhiteListMethod(List<String> receiverWhiteList){
        Set<String> whiteListMethodList = new HashSet<>();
        for (String receiver : receiverWhiteList){
            try{
                Class clazz = Class.forName(receiver);
                Method[] methods = clazz.getDeclaredMethods();
                for (Method method : methods){
                    whiteListMethodList.add(String.format("%s#%s", receiver, method.getName()));
                }
            }catch (Exception e){
                throw new RuntimeException(e);
            }
        }

        return whiteListMethodList;
    }
}
```
2. 根据下面的代码创建`AnnotationWhitelistCustomizer`对Annotation进行检查，防止通过MetaProgramming进行攻击
```java
import org.codehaus.groovy.ast.AnnotationNode;
import org.codehaus.groovy.ast.ClassNode;
import org.codehaus.groovy.classgen.GeneratorContext;
import org.codehaus.groovy.control.CompilationFailedException;
import org.codehaus.groovy.control.CompilePhase;
import org.codehaus.groovy.control.SourceUnit;
import org.codehaus.groovy.control.customizers.CompilationCustomizer;

import java.util.List;


public class AnnotationWhitelistCustomizer extends CompilationCustomizer {

    public AnnotationWhitelistCustomizer(){
        // 必须在CONVERSION阶段，否则不生效
        this(CompilePhase.CONVERSION);
    }

    public AnnotationWhitelistCustomizer(CompilePhase phase) {
        super(phase);
    }

    @Override
    public void call(SourceUnit source, GeneratorContext context, ClassNode classNode) throws CompilationFailedException {
       List<AnnotationNode> annotationNodeList = classNode.getAnnotations();
       if (!annotationNodeList.isEmpty()){
           throw new SecurityException("Can't Have MetaProgramming");
       }
    }
}
```
3. 给CompilerConfiguration配置WhiteListSecureASTCustomizer和AnnotationWhitelistCustomizer
```java
CompilerConfiguration compilerConfiguration = new CompilerConfiguration();

// 添加安全自定义器
WhiteListSecureASTCustomizer secureCustomizer = new WhiteListSecureASTCustomizer();
AnnotationWhitelistCustomizer annotationCustomizer = new AnnotationWhitelistCustomizer();
compilerConfiguration.addCompilationCustomizers(secureCustomizer);
compilerConfiguration.addCompilationCustomizers(annotationCustomizer);
```