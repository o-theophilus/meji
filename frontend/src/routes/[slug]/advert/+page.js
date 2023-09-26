export const load = async ({ fetch, params, parent }) => {

	let a = await parent();
	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert/${params.slug}`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});

	resp = await resp.json();

	if (resp.status == 200) {
		return resp
	}
}
