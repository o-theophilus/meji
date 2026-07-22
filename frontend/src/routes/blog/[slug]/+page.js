import { app } from "$lib/store.svelte.js";
import { error } from '@sveltejs/kit';

export const load = async ({ fetch, params, parent }) => {
    if (app.blog.slug == params.slug) return { blog: app.blog }

    let a = await parent();
    let response = await fetch(`${import.meta.env.VITE_BACKEND}/blogs/${params.slug}`, {
        headers: {
            'Content-Type': 'application/json',
            Authorization: a.locals.token
        },
    });
    let result = await response.json();

    if (response.status == 200) {
        return result
    } else {
        throw error(result.status, result.error)
    }
}