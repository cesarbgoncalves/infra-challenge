<?php

use App\Http\Controllers\Api\V1\Product\ProductListController;
use Illuminate\Support\Facades\Route;

Route::get('/v1/products', ProductListController::class);
