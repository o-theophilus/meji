import { get } from 'svelte/store';
import { loading, user } from "$lib/store.js"
import { token } from "$lib/cookie.js"
import { redirect, error } from '@sveltejs/kit';




export const load = async ({ parent, fetch, url }) => {
	
	let  a = await parent();
	if(!a.locals.user.login){
		throw redirect(307, `/?module=login&return_url=${url.pathname}`);
	}
	else if(!a.locals.user.roles.includes('admin')){
		throw error(400, 'not an admin')
	}

	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/admin/photos`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: get(token)
		}
	});
	resp = await resp.json();

	if (resp.status == 200) {
		return resp
    }
}
