<script context="module">
	export async function load({ url, session }) {
		if (session.user.login) {
			let order_key = url.searchParams.get('order_key');
			if (order_key) {
				return {
					status: 302,
					redirect: `/order/${order_key}?status=success`
				};
			}

			let ref = url.searchParams.get('reference');

			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}/order_ref/${ref}`, {
				method: 'get',
				headers: {
					'Content-Type': 'application/json',
					Authorization: session.token
				}
			});

			if (_resp.ok) {
				let resp = await _resp.json();

				if (resp.status == 200) {
					return {
						status: 302,
						redirect: `/order/${resp.data.order.key}?status=success`
					};
				}
				// else {
				// 	return {
				// 		// status: 404,
				// 		// error: resp.message
				// 	};
				// }
			}
		}
		return {
			status: 302,
			redirect: `/?module=login&return_url=${url.pathname}`
		};
	}
</script>
