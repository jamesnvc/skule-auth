<?php
setcookie('username', "", time()-3600, '/~james');
setcookie('sid', "", time()-3600, '/~james');
header('Location: http://localhost/~james/testing/test1.php');
?>