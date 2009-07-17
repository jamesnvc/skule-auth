<html>
<head><title>Test 2</title></head>
<body>
<pre>
<?php
print_r($_COOKIE);
?>
</pre>
<?php if ($_POST['bar'] == $_COOKIE['sid']) { ?>
<p>You entered <? echo $_POST['foo'] ?></p>
<?php } else { ?>
<p>Authentication error!</p>
<?php } ?>
</body>
</html>