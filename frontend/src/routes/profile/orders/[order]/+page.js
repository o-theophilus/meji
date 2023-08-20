import { loading } from "$lib/store.js"

export const load = async ({ fetch, params, parent }) => {

	let  a = await parent();
	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order/${params.order}`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	resp = await resp.json();
	loading.set(false)

	if (resp.status == 200) {
		return resp
    }
}
