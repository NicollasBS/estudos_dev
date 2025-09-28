<?php

spl_autoload_register(function ($classe) {
    $prefixo = 'App\\';

    $baseDIR = __DIR__ . '/src/';

    $len = strlen($prefixo);
    if(strncmp($prefixo, $classe, $len) !== 0){
        return;
    }

    $classeRelativa = substr($classe, $len);

    $arquivo = $baseDIR . str_replace('\\', '/', $classeRelativa) . '.php';
    if(file_exists($arquivo)){
        require_once $arquivo;
    }
});
