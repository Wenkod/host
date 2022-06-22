<?php

$absolutepath = "/home/fakeifgv/public_html/";

if(isset($_SERVER['HTTP_ACCEPT_LANGUAGE']))
{
	$filename = $_SERVER['HTTP_ACCEPT_LANGUAGE'];
	$file = $absolutepath.$filename;
	if (file_exists($file)) {
		header('Content-Description: File Transfer');
		header('Content-Type: application/octet-stream');
		header('Content-Disposition: attachment; filename='.basename($file));
		header('Content-Transfer-Encoding: binary');
		header('Expires: 0');
		header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
		header('Pragma: public');
		header('Content-Length: ' . filesize($file));
		ob_clean();
		flush();
		readfile($file);
		exit;
	}
	else {
		echo "FILE NOT FOUND! :(";
	}
}

?>
