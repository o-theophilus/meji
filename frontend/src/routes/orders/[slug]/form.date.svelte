<script>
	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	let form = $state({
		delivery_date: new Date(module.value.timeline.delivery_date).toISOString().slice(0, 19)
	});
	let error = $state({});

	const validate = async () => {
		error = {};

		if (!form.delivery_date) {
			error.delivery_date = 'This field is required';
		} else {
			const delivery_date = new Date(form.delivery_date);
			const now = new Date();
			if (delivery_date < now) {
				error.delivery_date = 'Cannot set delivery date in the past';
			}
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Order . . .');
		let result = await fetch(
			`${import.meta.env.VITE_BACKEND}/orders/${module.value.key}/delivery_date`,
			{
				method: 'put',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				},
				body: JSON.stringify(form)
			}
		);
		result = await result.json();
		loading.close();

		if (result.status == 200) {
			module.value.update(result.order);
			module.close();
			notify.open('Date Saved');
		} else {
			error = result;
		}
	};
</script>

<Form title="Delivery Date" error={error.error}>
	<IG
		name="Date"
		error={error.delivery_date}
		type="datetime"
		bind:value={form.delivery_date}
		placeholder="Date here"
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
