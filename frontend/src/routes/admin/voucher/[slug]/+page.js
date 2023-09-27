import { loading } from "$lib/store.js"

export const load = async ({ fetch, parent,params }) => {
	let  a = await parent();
	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/voucher/${params.slug}`, {
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
