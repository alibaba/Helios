为了防止命令注入漏洞可以使用命令参数的形式，禁止直接将参数拼接到命令中。
1. 应使用数组的方式传递命令和参数，例如在ProcessBuilder中使用传递 new String{"curl", "www.baidu.com"}
2. 如果需要需要管道处理或者重定向，应在代码中获取对应的输入输出后，传递到第二个Process的stdin中，或复制流到文件中。
3. 如果必须使用bash -c的场景，应保证用户无法操作bash脚本的ast。比如假如dir和keyword由用户传入，应禁止 `{"bash", "-c", String.format("ls -al %s | grep %s", dir, keyword)}` 要改写成`{"bash", "-c", "ls -al \"$0\" | grep \"$1\"", dir, keyword)}` 通过bash参数传递，将参数和命令分离开。其中$0表示传入的第一个参数，$1表示传入的第二个参数。