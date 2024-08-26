<?php

namespace App\Http\Requests\Api\V1\Product;

use Illuminate\Foundation\Http\FormRequest;

class ProductListRequest extends FormRequest
{

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'page' => [
                'nullable',
                'int'
            ],
            'perPage' => [
                'nullable',
                'int',
                'min:50',
                'max:1000',
            ]
        ];
    }
}
