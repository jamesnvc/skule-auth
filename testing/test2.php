<?php
session_id($_POST['phpses']);
session_start();
?>
<html>
<head>
<title>Test 2</title>
  <link rel="stylesheet" href="/~james/css/bluetrip/screen.css" type="text/css" media="screen, projection"/>
  <link rel="stylesheet" href="/~james/css/bluetrip/print.css" type="text/css" media="print"/> 
  <!--[if IE]>
      <link rel="stylesheet" href="/~james/css/bluetrip/ie.css" type="text/css" media="screen, projection"/>
      <![endif]-->
  <link rel="stylesheet" href="/~james/css/bluetrip/style.css" type="text/css" media="screen, projection"/>
</head>
<body>
<div class="container">
<?php if ( isset($_COOKIE['sid']) && $_POST['bar'] == hash('sha256', $_COOKIE['sid'] . $_SESSION['rand_val'])) { ?>
<p>You entered <? echo $_POST['foo'] ?></p>
<?php } else { ?>
<p>Authentication error!</p>
<p><a href="./test1.php">Try again?</a></p>
<?php } ?>
</div>
</body>
</html>
<?php
unset($_SESSION['rand_val']);
session_destroy();
?>