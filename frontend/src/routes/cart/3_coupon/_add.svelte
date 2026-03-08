<script>
	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';

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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart/coupon`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			notify.open('Coupon Added');
			module.value.ops.coupon = resp.coupon;
			module.close();
		} else {
			error = resp;
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
