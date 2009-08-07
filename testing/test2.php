<html>
<head><title>Test 2</title></head>
<body>
<pre>
<?php
print_r($_COOKIE);
?>
</pre>
<?php if (isset($_COOKIE['sid']) && $_POST['bar'] == $_COOKIE['sid'] ) { ?>
<p>You entered <? echo $_POST['foo'] ?></p>
<?php } else { ?>
<p>Authentication error!</p>
<p><a href="./test1.php">Try again?</a></p>
<?php } ?>
</body>
</html>