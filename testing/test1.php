<?php
session_start();
unset($_SESSION['rand_val']);
$_SESSION['rand_val'] = rand();
?>
<html>
<head>
  <title>Test 1</title>
  <link rel="stylesheet" href="/~james/css/bluetrip/screen.css" type="text/css" media="screen, projection"/>
  <link rel="stylesheet" href="/~james/css/bluetrip/print.css" type="text/css" media="print"/> 
  <!--[if IE]>
      <link rel="stylesheet" href="/~james/css/bluetrip/ie.css" type="text/css" media="screen, projection"/>
      <![endif]-->
  <link rel="stylesheet" href="/~james/css/bluetrip/style.css" type="text/css" media="screen, projection"/>
</head>
<body>
  <div class="container">
  <h1>Test One:</h1>
  <?php if (isset($_COOKIE['username'])) { ?>
   <p>Hello, <? echo $_COOKIE['username'] ?>!</p>
   <p><form action="logout.php" method="POST"><input type="submit" value="Logout"/></form></p>
<?php    } else { ?>
   <p>Please <a href="./login.html">Login</a></p>
     <?php } ?>
<h2>Enter Something</h2>
<form action="test2.php" method="POST">
   <label title="A string" for="foo">String:</label>
   <input type="text" name="foo" />
   <input type="hidden" name="bar" value="<?php echo hash('sha256', $_COOKIE['sid'] . $_SESSION['rand_val'])?>"/>
   <input type="hidden" name="phpses" value="<?php echo session_id(); ?>"/>
   <input type="submit" value="done" />
 </form>
</div>
</body>
</html>