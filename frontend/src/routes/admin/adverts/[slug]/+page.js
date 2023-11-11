export const load = async ({ fetch, params, parent }) => {

	let a = await parent();
	if (!a.locals.user.roles.includes("item:advert")) {
		throw error(400, "unauthorized access")
	}

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
