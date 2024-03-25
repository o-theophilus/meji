export const load = async ({ fetch, parent, url }) => {

	let a = await parent();
	if (!a.locals.user.login) {
		throw redirect(307, `/?module=login&return_url=${url.pathname}`);
	}

	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/transaction`, {
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
