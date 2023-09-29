import { redirect, error } from '@sveltejs/kit';
import { loading } from "$lib/store.js"

export const load = async ({ parent, fetch, url }) => {
	let a = await parent();
	if (!a.locals.user.login) {
		throw redirect(307, `/?module=login&return_url=${url.pathname}`);
	}
	else if (!a.locals.user.roles.includes('admin')) {
		throw error(400, 'not an admin')
	}

	let backend = new URL(`${import.meta.env.VITE_BACKEND}/user`)
	if (url.search) {
		backend.search = url.search
	}

	let resp = await fetch(backend.href, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	resp = await resp.json();
	loading.set(false)
	return resp
}
