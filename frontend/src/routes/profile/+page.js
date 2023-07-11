import { redirect } from '@sveltejs/kit';

export const load = async ({ parent }) => {
	let  a  = await parent();
	if(!a.locals.user.login){
		throw redirect(307, `/?module=login&return_url=${url.pathname}`);
	}
}
