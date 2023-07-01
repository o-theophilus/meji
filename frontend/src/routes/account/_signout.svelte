<script>
	import { token } from '$lib/cookie.js';
	import { user, import.meta.env.VITE_BACKEND } from '$lib/store.js';


	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}logout`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$token = resp.data.token;
				$user = resp.data.user;

				document.location = '/';
			}
		}
	};
</script>

<slot {submit} />
