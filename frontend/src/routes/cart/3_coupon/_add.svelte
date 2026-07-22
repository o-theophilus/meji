<script>
	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify, page_state } from '$lib/store.svelte.js';

	let form = $state({ code: '' });
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.code) {
			error.code = 'This field is required';
		} else if (form.code.length != 10) {
			error.code = 'This field must be 10 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Adding Coupon . . .');
		let result = await fetch(`${import.meta.env.VITE_BACKEND}/cart/coupon`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		result = await result.json();
		loading.close();

		if (result.status == 200) {
			notify.open('Coupon Added');
			module.value.ops.coupon = result.coupon;
			page_state.state['cart'].data.coupon = result.coupon;
			module.close();
		} else {
			error = result;
		}
	};
</script>

<Form title="Add Coupon" error={error.error}>
	<IG
		name="Code"
		icon="user"
		error={error.code}
		placeholder="Code here"
		type="text"
		bind:value={form.code}
		required
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
