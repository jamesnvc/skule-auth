<?php
// Use a session to store the random value between pages
session_start();
$_SESSION['rand_val'] = rand();
?>
<html>
<head><title>Test 1</title></head>
<body>
<pre>
<?php
print_r($_COOKIE);
?>
</pre>
<p>Test One:
<?php if (isset($_COOKIE['username'])) { ?>
   <p>Hello, <? echo $_COOKIE['username'] ?>!</p>
<?php    } else { ?>
   <p>Please <a href="./login.html">Login</a></p>
     <?php } ?>
<form action="test2.php" method="POST">
   <label title="A string" for="foo">String:
      <input type="text" name="foo" />
   </label>
   <input type="hidden" name="bar" value="<?php echo $_COOKIE['sid'] ?>"/>
   <input type="submit" value="done" />
</form>
</p>
</body>
</html>