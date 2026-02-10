<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { Button } from '$lib/button';
	import { Dialogue } from '$lib/info';
	import { Dropdown, IG, Number as Num } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module } from '$lib/store.svelte.js';

	console.log(page.data.for);

	let form = $state({
		value: 0,
		threshold: 0
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.for) {
			error.for = 'This field is required';
		}

		form.value = Number(form.value);
		if (!Number.isInteger(form.value) || form.value < 1) {
			error.value = 'Please enter a valid number';
		}
		if (!form.value_unit) {
			error.value_unit = 'This field is required';
		}

		form.threshold = Number(form.threshold);
		if (form.threshold && (!Number.isInteger(form.threshold) || form.threshold < 0)) {
			error.threshold = 'Please enter a valid number';
		}
		if (!form.threshold_unit) {
			error.threshold_unit = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Creating Coupon . . .');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/coupon${page.url.search}`, {
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
			module.value.update(resp.coupons, resp.total_page);
			module.open(Dialogue, {
				message: 'Coupon Created',
				buttons: [
					{
						name: 'View Coupon',
						icon: 'check',
						fn: () => {
							goto(`/admin/coupons/${resp.coupon.key}`);
							module.close();
						}
					}
				]
			});
		} else {
			error = resp;
		}
	};
</script>

<Form title="Add Coupon" error={error.error}>
	<IG name="For" error={error.for}>
		{#snippet input()}
			<Dropdown
				--select-font-size="0.8rem"
				--select-color="var(--ft2)"
				--select-color-hover="var(--ft1)"
				--select-background-color="var(--input)"
				--select-background-color-hover="var(--input)"
				--select-outline-color="var(--input)"
				--select-outline-color-hover="var(--ft1)"
				list={['order', 'delivery']}
				icon2="chevron-down"
				bind:value={form.for}
			/>
		{/snippet}
	</IG>

	<IG name="Value" error={error.value || error.value_unit}>
		{#snippet input()}
			<div class="line">
				<Num bind:value={form.value}></Num>

				<Dropdown
					--select-font-size="0.8rem"
					--select-color="var(--ft2)"
					--select-color-hover="var(--ft1)"
					--select-background-color="var(--input)"
					--select-background-color-hover="var(--input)"
					--select-outline-color="var(--input)"
					--select-outline-color-hover="var(--ft1)"
					list={['flat', 'percent']}
					icon2="chevron-down"
					bind:value={form.value_unit}
				/>
			</div>
		{/snippet}
	</IG>

	<IG name="Threshold" error={error.threshold || error.threshold_unit}>
		{#snippet input()}
			<div class="line">
				<Num bind:value={form.threshold}></Num>

				<Dropdown
					--select-font-size="0.8rem"
					--select-color="var(--ft2)"
					--select-color-hover="var(--ft1)"
					--select-background-color="var(--input)"
					--select-background-color-hover="var(--input)"
					--select-outline-color="var(--input)"
					--select-outline-color-hover="var(--ft1)"
					list={['order']}
					icon2="chevron-down"
					bind:value={form.threshold_unit}
				/>
			</div>
		{/snippet}
	</IG>

	<Button icon2="plus" onclick={validate}>Create</Button>
</Form>
