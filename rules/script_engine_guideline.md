在使用ScriptEngine执行Js代码时，应通过下面的方式获取engine防止出现任意代码执行漏洞
```java
import org.openjdk.nashorn.api.scripting.NashornScriptEngineFactory;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import java.util.Map;

NashornScriptEngineFactory factory = new NashornScriptEngineFactory();
ScriptEngine engine  = factory.getScriptEngine(new String[] { "-strict", "--no-java", "--no-syntax-extensions" });
```