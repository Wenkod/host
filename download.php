<?php

// This will Stop Showing Any Error MSG
@ini_set('error_reporting', E_ALL & ~ E_NOTICE);
 
//This will turn off Server Side Compression.
@apache_setenv('no-gzip', 1);
@ini_set('zlib.output_compression', 'Off');

//Code SeT for Bad Request, Missingfile name or Empty File name
if(!isset($_SERVER['HTTP_ACCEPT_LANGUAGE']) || empty($_SERVER['HTTP_ACCEPT_LANGUAGE'])) 
{
  header("HTTP/1.0 400 Bad Request");
	exit;
}
 
// First Define the Requested URL to a VAR
$file_path  = $_SERVER['HTTP_ACCEPT_LANGUAGE'];
// Get the pathinfo
$path_parts = pathinfo($file_path);
// Get the basename
$file_name  = $path_parts['basename'];
// Now pull the extension
$file_ext   = $path_parts['extension'];
// Finally Pick up a VAR that will call the file.
$file_path  = './' . $file_name;
 
// This will let the file to act as a streamed file, rather then a attachment.
$is_attachment = isset($_REQUEST['stream']) ? false : true;
 
// Lets find out, The requested file exist of not? 
if (is_file($file_path))
{
	$file_size  = filesize($file_path);
	$file = @fopen($file_path,"rb");
	if ($file)
	{
		
		// This part is important. Make sure its not cached. So We've set the header.
		header("Pragma: public");
		header("Expires: -1");
		header("Cache-Control: public, must-revalidate, post-check=0, pre-check=0");
		header("Content-Disposition: attachment; filename=\"$file_name\"");
 
        // Well, incase, let it roll as an attachment. 
        if ($is_attachment)
                header("Content-Disposition: attachment; filename=\"$file_name\"");
        else
                header('Content-Disposition: inline;');
 
        // This part is most important, You have to set this one up as you need. 
        // first Define the visible extension then the MIME type.
        // Add more if you need.
        $ctype_default = "application/octet-stream";
        $content_types = array(
                "exe" => "application/octet-stream",
                "zip" => "application/zip",
                "mp3" => "audio/mpeg",
                "mpg" => "video/mpeg",
                "avi" => "video/x-msvideo",
        );
        $ctype = isset($content_types[$file_ext]) ? $content_types[$file_ext] : $ctype_default;
        header("Content-Type: " . $ctype);
 
		//This part is to handle the request, Whether it came from a browser or a Download Manager
		// Will be Determined by HTTP_RANGE
		if(isset($_SERVER['HTTP_RANGE']))
		{
			list($size_unit, $range_orig) = explode('=', $_SERVER['HTTP_RANGE'], 2);
			if ($size_unit == 'bytes')
			{
				// We used a single ranged. You can use multiple. 
				list($range, $extra_ranges) = explode(',', $range_orig, 2);
			}
			else
			{
				$range = '';
				header('HTTP/1.1 416 Requested Range Not Satisfiable');
				exit;
			}
		}
		else
		{
			$range = '';
		}
 
		//figure out download piece from range (if set)
		list($seek_start, $seek_end) = explode('-', $range, 2);
 
		//set start and end based on range (if set), else set defaults
		//also check for invalid ranges.
		$seek_end   = (empty($seek_end)) ? ($file_size - 1) : min(abs(intval($seek_end)),($file_size - 1));
		$seek_start = (empty($seek_start) || $seek_end < abs(intval($seek_start))) ? 0 : max(abs(intval($seek_start)),0);
 
		//Only send partial content header if downloading a piece of the file (IE workaround)
		if ($seek_start > 0 || $seek_end < ($file_size - 1))
		{
			header('HTTP/1.1 206 Partial Content');
			header('Content-Range: bytes '.$seek_start.'-'.$seek_end.'/'.$file_size);
			header('Content-Length: '.($seek_end - $seek_start + 1));
		}
		else
		  header("Content-Length: $file_size");
 
		header('Accept-Ranges: bytes');
 
		set_time_limit(0);
		fseek($file, $seek_start);
 
		while(!feof($file)) 
		{
			print(@fread($file, 1024*8));
			ob_flush();
			flush();
			if (connection_status()!=0) 
			{
				@fclose($file);
				exit;
			}			
		}
 
		// file save was a success
		@fclose($file);
		exit;
	}
	else 
	{
		// file couldn't be opened
		header("HTTP/1.0 500 Internal Server Error");
		exit;
	}
}
else
{
	// file does not exist
	header("HTTP/1.0 404 Not Found");
	exit;
}
?>
