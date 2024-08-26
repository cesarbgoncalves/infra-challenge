<?php

namespace App\Http\Controllers\Api\V1\Product;

use App\Http\Controllers\Controller;
use App\Http\Requests\Api\V1\Product\ProductListRequest;
use App\Http\Resources\Api\V1\Product\ProductListResource;
use App\Models\Product;

class ProductListController extends Controller
{
    /**
     * Handle the incoming request.
     */
    public function __invoke(ProductListRequest $request)
    {
        $products = Product::query()
            ->paginate($request->validated('perPage', 100));

        return ProductListResource::collection($products);
    }
}
