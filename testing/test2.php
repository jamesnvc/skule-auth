<?php
session_id($_POST['phpses']);
session_start();
?>
<html>
<head><title>Test 2</title></head>
<body>
<pre>
<?php
echo 'COOKIE:';
print_r($_COOKIE);
echo 'SESSION:';
print_r($_SESSION);
?>
</pre>
<?php if ( isset($_COOKIE['sid']) && $_POST['bar'] == hash('sha256', $_COOKIE['sid'] . $_SESSION['rand_val'])) { ?>
<p>You entered <? echo $_POST['foo'] ?></p>
<?php } else { ?>
<p>Authentication error!</p>
<p><a href="./test1.php">Try again?</a></p>
<?php } ?>
</body>
</html>
<?php
unset($_SESSION['rand_val']);
session_destroy();
?>