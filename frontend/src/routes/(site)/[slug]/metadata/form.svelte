<script>
	import { page } from '$app/state';
	import { Button } from '$lib/button';
	import { Dropdown, IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	let form = $state({
		length: module.value.length,
		breadth: module.value.breadth,
		height: module.value.height,
		weight: module.value.weight,
		area: module.value.area,
		address: module.value.address
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (form.length && (!Number.isInteger(form.length) || form.length < 0)) {
			error.length = 'Please enter a valid number';
		} else if (form.length == module.value.length) {
			error.length = 'No changes were made';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Item . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/items/${module.value.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ metadata: form })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.item);
			notify.open('Metadata Saved');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form
	title="Edit Metadata"
	description="This information is used to determine the delivery cost"
	error={error.error}
>
	<IG
		name="Length (cm)"
		error={error.length}
		placeholder="Length (cm) here"
		type="number"
		bind:value={form.length}
	/>

	<IG
		name="Breadth (cm)"
		error={error.breadth}
		placeholder="Breadth (cm) here"
		type="number"
		bind:value={form.breadth}
	/>

	<IG
		name="Height (cm)"
		error={error.height}
		placeholder="Height (cm) here"
		type="number"
		bind:value={form.height}
	/>

	<IG
		name="Weight (kg)"
		error={error.weight}
		placeholder="Weight (kg) here"
		type="number"
		bind:value={form.weight}
	/>

	<IG
		name="Address"
		icon="map-pin"
		error={error.address}
		placeholder="Address here"
		type="text"
		bind:value={form.address}
	/>

	<IG name="Area" error={error.area}>
		{#snippet input()}
			<Dropdown icon="map-pin" list={page.data.areas} bind:value={form.area}></Dropdown>
		{/snippet}
	</IG>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
