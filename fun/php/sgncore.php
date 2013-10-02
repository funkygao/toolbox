<?php
class sgncore {

	public static function init() {
		register_shutdown_function(array(__CLASS__, 'shutdown_handler'));
		set_exception_handler(array(__CLASS__, 'exception_handler'));
		set_error_handler(array(__CLASS__, 'error_handler'));
	}

	public static function error_handler($code, $error, $file = NULL, $line = NULL) {
		$exception = new ErrorException($error, $code, 0, $file, $line);
        if (E_ERROR & $code) {
            echo "Runtime error: $code\n";
            print_r($exception);
		} else if (error_reporting() & $code) {
			echo "Catchable error: $code, $error, $file, $line\n";
		}

		return TRUE;
	}

    public static function exception_handler(Exception $e) {
        echo "Exception $e\n";

		return TRUE;
	}

	public static function shutdown_handler() {
		//echo('shutdown');
		if ($error = error_get_last()) {
			self::exception_handler(new ErrorException($error['message'], $error['type'], 0, $error['file'], $error['line']));
		}
	}
}

