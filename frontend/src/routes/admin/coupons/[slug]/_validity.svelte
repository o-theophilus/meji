<script>
	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify, page_state } from '$lib/store.svelte.js';

	const get_date = (days = 0) => {
		const d = new Date();
		d.setDate(d.getDate() + days);
		return d.toISOString().split('T')[0];
	};

	let form = $state({
		// valid_from: get_date(),
		// valid_until: get_date(30)
	});

	if (module.value.coupon.valid_from) {
		form.valid_from = new Date(module.value.coupon.valid_from).toISOString().split('T')[0];
	} else {
		form.valid_from = get_date();
	}
	if (module.value.coupon.valid_until) {
		form.valid_until = new Date(module.value.coupon.valid_until).toISOString().split('T')[0];
	} else {
		form.valid_until = get_date(30);
	}

	let error = $state({});

	const validate = async () => {
		error = {};

		if (!form.valid_from) {
			error.valid_from = 'This field is required';
		} else if (valid_from < get_date()) {
			error.valid_from = 'Cannot set date in the past';
		}

		if (!form.valid_until) {
			error.valid_until = 'This field is required';
		} else if (form.valid_from && form.valid_until <= form.valid_from) {
			error.valid_until = 'Cannot set date earlier or equal to start date';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Updating Validity . . .');
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/coupons/${module.value.coupon.key}/validity`,
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
			page_state.clear('coupons');
			module.value.update(resp.coupon);
			module.close();
			notify.open('Validity Updated');
		} else {
			error = resp;
		}
	};

	const clear = async () => {
		loading.open('Removing Validity . . .');
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/coupons/${module.value.coupon.key}/validity`,
			{
				method: 'delete',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				}
			}
		);
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.coupon);
			module.close();
			notify.open('Validity Removed');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Validity" error={error.error}>
	<IG
		name="Valid From"
		error={error.valid_from}
		type="date"
		min={get_date()}
		bind:value={form.valid_from}
		placeholder="Date here"
	/>

	<IG
		name="Valid Until"
		error={error.valid_until}
		type="date"
		min={get_date(1)}
		bind:value={form.valid_until}
		placeholder="Date here"
	/>

	<div class="line">
		<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
		{#if module.value.coupon.valid_from || module.value.coupon.valid_until}
			<Button icon2="send-horizontal" onclick={clear}>Clear</Button>
		{/if}
	</div>
</Form>
