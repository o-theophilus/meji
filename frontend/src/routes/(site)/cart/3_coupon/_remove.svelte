<script>
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify, page_state } from '$lib/store.svelte.js';

	let error = $state({});

	const submit = async () => {
		loading.open('Removing Coupon . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart/coupon`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			notify.open('Coupon Removed');
			module.value.ops.coupon = resp.coupon;
			page_state.state['cart'].data.coupon = resp.coupon;
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Remove Coupon" error={error.error}>
	<Button icon2="send-horizontal" onclick={() => module.close()}>Cancel</Button>
	<Button icon2="send-horizontal" onclick={submit}>Remove</Button>
</Form>
