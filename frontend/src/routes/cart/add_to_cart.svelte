<script>
	import { module, loading, notify, app, page_state } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import Value from '../[slug]/variation/value.svelte';

	let item = { ...module.value };
	let form = $state({
		key: item.key,
		quantity: 1,
		variation: {},
		operation: 'add'
	});
	let error = $state({});

	const validate = () => {
		error = {};
		if (form.quantity && (!Number.isInteger(form.quantity) || form.quantity < 1)) {
			error.quantity = 'Please enter a valid number';
		}

		for (const [key, val] of Object.entries(item.variation)) {
			if (!form.variation[key] || !val.includes(form.variation[key])) {
				error[key] = `Please select a ${key}`;
			}
		}

		Object.keys(error).length === 0 && submit();
	};

	const pre_modify = async () => {
		let exists = false;
		for (const x of app.cart_items) {
			if (x.key == form.key && JSON.stringify(x.variation) == JSON.stringify(form.variation)) {
				exists = true;
				break;
			}
		}

		if (!exists) {
			app.cart_items = [
				...app.cart_items,
				{
					key: item.key,
					name: item.name,
					photo: item.files.length ? item.files[0] : null,
					price: item.price,
					slug: item.slug,
					status: item.status,
					quantity: form.quantity,
					variation: JSON.parse(JSON.stringify(form.variation))
				}
			];
		}
	};

	const reverse_modify = async () => {
		app.cart_items = app.cart_items.filter(
			(x) => !(x.key == form.key && JSON.stringify(x.variation) == JSON.stringify(form.variation))
		);
	};

	const submit = async () => {
		pre_modify();
		loading.open('Adding item to cart . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();
		console.log(resp);

		if (resp.status == 200) {
			app.cart_items = resp.items;
			notify.open('Item added to cart');
			module.close();
			page_state.clear('cart');
		} else {
			reverse_modify();
			error = resp;
		}
	};
</script>

<Form title="Add to Cart" description="Select variation" error={error.error}>
	{#each Object.entries(item.variation) as [key, values]}
		<IG name={key} error={error[key]}>
			{#snippet input()}
				<div class="line">
					{#each values as value}
						<Value
							active={form.variation[key] == value}
							{value}
							onclick={() => {
								form.variation[key] = value;
							}}
						></Value>
					{/each}
				</div>
			{/snippet}
		</IG>
	{/each}

	<IG name="Quantity" error={error.quantity} type="number" bind:value={form.quantity} />

	<Button icon="cart" onclick={validate}>Add to Cart</Button>
</Form>
