<?php

namespace App\Providers;

use Illuminate\Http\Resources\Json\AnonymousResourceCollection;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        AnonymousResourceCollection::macro('paginationInformation', function ($request, $paginated, $default) {
            unset($default['links'], $default['meta']['links']);
            return $default;
        });
    }
}
