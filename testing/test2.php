<html>
<head>
<title>Test 2</title>
</head>
<body>
<?php if ($_POST['bar'] == "aoeu") { ?>
<p>You entered <? echo $_POST['foo'] ?></p>
<?php } else { ?>
<p>Authentication error!</p>
<?php } ?>
</body>
</html>