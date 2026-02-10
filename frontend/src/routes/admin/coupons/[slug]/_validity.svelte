<script>
	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	let form = $state({});
	if (module.value.coupon.valid_from) {
		form.valid_from = new Date(module.value.coupon.valid_from).toISOString().slice(0, 19);
	} else {
		form.valid_from = new Date().toISOString().slice(0, 19);
	}
	if (module.value.coupon.valid_until) {
		form.valid_until = new Date(module.value.coupon.valid_until).toISOString().slice(0, 19);
	} else {
		form.valid_until = new Date().toISOString().slice(0, 19);
	}
	let error = $state({});

	const validate = async () => {
		error = {};

		if (!form.valid_from) {
			error.valid_from = 'This field is required';
		}

		if (!form.valid_until) {
			error.valid_until = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Updating Validity . . .');
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/coupon/validity/${module.value.coupon.key}`,
			{
				method: 'put',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				},
				body: JSON.stringify(form)
			}
		);
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.coupon);
			module.close();
			notify.open('Validity Updated');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Validity" error={error.error}>
	<IG
		name="Valid From"
		error={error.valid_from}
		type="datetime"
		bind:value={form.valid_from}
		placeholder="Date here"
	/>

	<IG
		name="Valid Until"
		error={error.valid_until}
		type="datetime"
		bind:value={form.valid_until}
		placeholder="Date here"
	/>

	<div class="line">
		<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
		<Button icon2="send-horizontal" onclick={validate}>Clear</Button>
	</div>
</Form>
