<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { Button } from '$lib/button';
	import { Dialogue } from '$lib/info';
	import { Dropdown, IG, Input } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module } from '$lib/store.svelte.js';

	let form = $state({
		value: 1,
		condition: 0
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.applies_to) {
			error.applies_to = 'This field is required';
		}

		form.value = Number(form.value);
		if (!Number.isInteger(form.value) || form.value < 1) {
			error.value = 'Please enter a valid number';
		}
		if (!form.value_unit) {
			error.value_unit = 'This field is required';
		}

		form.condition = Number(form.condition);
		if (form.condition && (!Number.isInteger(form.condition) || form.condition < 0)) {
			error.condition = 'Please enter a valid number';
		}
		if (!form.condition_unit) {
			error.condition_unit = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Creating Coupon . . .');

		let result = await fetch(`${import.meta.env.VITE_BACKEND}/coupons${page.url.search}`, {
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
			module.value.update(result.coupons, result.total_page);
			module.open(Dialogue, {
				message: 'Coupon Created',
				buttons: [
					{
						name: 'View Coupon',
						icon: 'check',
						fn: () => {
							goto(`/admin/coupons/${result.coupon.key}`);
							module.close();
						}
					}
				]
			});
		} else {
			error = result;
		}
	};
</script>

<Form title="Add Coupon" error={error.error}>
	<IG name="Applies to" error={error.applies_to}>
		{#snippet input()}
			<Dropdown
				--select-font-size="0.8rem"
				--select-color="var(--ft2)"
				--select-color-hover="var(--ft1)"
				--select-background-color="var(--input)"
				--select-background-color-hover="var(--input)"
				--select-outline-color="var(--input)"
				--select-outline-color-hover="var(--ft1)"
				list={page.data.applies_to}
				icon2="chevron-down"
				bind:value={form.applies_to}
			/>
		{/snippet}
	</IG>

	<IG name="Value" error={error.value || error.value_unit}>
		{#snippet input()}
			<div class="line">
				<Input
					min="1"
					max={form.value_unit == 'percent' ? 100 : undefined}
					type="number"
					bind:value={form.value}
				></Input>

				<Dropdown
					--select-font-size="0.8rem"
					--select-color="var(--ft2)"
					--select-color-hover="var(--ft1)"
					--select-background-color="var(--input)"
					--select-background-color-hover="var(--input)"
					--select-outline-color="var(--input)"
					--select-outline-color-hover="var(--ft1)"
					list={page.data.value_unit}
					icon2="chevron-down"
					bind:value={form.value_unit}
					onchange={(e) => {
						if (e == 'percent' && form.value > 100) {
							form.value = 100;
						}
					}}
				/>
			</div>
		{/snippet}
	</IG>

	<IG name="condition" error={error.condition || error.condition_unit}>
		{#snippet input()}
			<div class="line">
				<Input type="number" bind:value={form.condition}></Input>

				<Dropdown
					--select-font-size="0.8rem"
					--select-color="var(--ft2)"
					--select-color-hover="var(--ft1)"
					--select-background-color="var(--input)"
					--select-background-color-hover="var(--input)"
					--select-outline-color="var(--input)"
					--select-outline-color-hover="var(--ft1)"
					list={page.data.condition_unit}
					icon2="chevron-down"
					bind:value={form.condition_unit}
				/>
			</div>
		{/snippet}
	</IG>

	<Button icon2="plus" onclick={validate}>Create</Button>
</Form>
