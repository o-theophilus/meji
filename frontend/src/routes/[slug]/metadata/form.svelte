<script>
	import { page } from '$app/state';
	import { Button } from '$lib/button';
	import { Dropdown, IG, Input } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	let form = $state({
		length: module.value.length,
		breadth: module.value.breadth,
		height: module.value.height,
		weight: module.value.weight,
		address: module.value.address,
		area: module.value.area,
		prep_time: module.value.prep_time
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (
			form.length == module.value.length &&
			form.breadth == module.value.breadth &&
			form.height == module.value.height &&
			form.weight == module.value.weight &&
			form.address == module.value.address &&
			form.area == module.value.area &&
			form.prep_time == module.value.prep_time
		) {
			error.error = 'No changes were made';
		}

		if (
			(form.length && (!Number.isFinite(form.length) || form.length < 0)) ||
			(form.breadth && (!Number.isFinite(form.breadth) || form.breadth < 0)) ||
			(form.height && (!Number.isFinite(form.height) || form.height < 0))
		) {
			error.dimension = 'Please enter a valid number';
		}
		if (form.weight && (!Number.isFinite(form.weight) || form.weight < 0)) {
			error.weight = 'Please enter a valid number';
		}
		if (form.prep_time && (!Number.isInteger(form.prep_time) || form.prep_time < 0)) {
			error.prep_time = 'Please enter a valid number';
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
	<IG name="Dimension (cm) Length, Breadth, Height" error={error.dimension}>
		{#snippet input()}
			<div class="line">
				<Input type="number" icon="ruler-dimension-line" bind:value={form.length} />
				<Input type="number" icon="ruler-dimension-line" bind:value={form.breadth} />
				<Input type="number" icon="ruler-dimension-line" bind:value={form.height} />
			</div>
		{/snippet}
	</IG>

	<IG
		name="Weight (kg)"
		error={error.weight}
		placeholder="Weight (kg) here"
		type="number"
		icon="scale"
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
			<Dropdown
				--select-color="var(--ft2)"
				--select-color-hover="var(--ft2)"
				--select-background-color="var(--input)"
				--select-background-color-hover="var(--input)"
				--select-outline-color="var(--input)"
				--select-outline-color-hover="var(--ft1)"
				--select-width="calc(100% - 2 * 16px)"
				--select-justify="left"
				--select-gap="16px"
				icon="map-pin"
				list={page.data.areas}
				bind:value={form.area}
			></Dropdown>
		{/snippet}
	</IG>

	<IG
		name="Prep Time (days)"
		icon="clock"
		error={error.prep_time}
		placeholder="Prep Time here"
		type="number"
		bind:value={form.prep_time}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>

<style>
	.line {
		flex-wrap: nowrap;
	}
</style>
