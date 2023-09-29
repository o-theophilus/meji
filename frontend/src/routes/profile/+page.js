import { redirect, error } from '@sveltejs/kit';
import { loading } from "$lib/store.js"

export const load = async ({ parent, fetch, url }) => {
	console.log("call backend");
	let a = await parent();
	if (!a.locals.user.login) {
		throw redirect(307, `/?module=login&return_url=${url.pathname}`);
	}
	else if (!a.locals.user.roles.includes('admin')) {
		throw error(400, 'not an admin')
	}

	let params = url.searchParams
	if (params.has("search")) {
		let search = params.get("search")
		
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${search}`, {
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
	loading.set(false)
	return { user: a.locals.user }
}
