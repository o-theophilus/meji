<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { Button } from '$lib/button';
	import { Dialogue } from '$lib/info';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module } from '$lib/store.svelte.js';
	let form = $state({});
	let error = $state({});

	const validate = () => {
		error = {};
		if (!form.name) {
			error.name = 'This field is required';
		} else if (form.name.length > 100) {
			error.name = 'This field cannot exceed 100 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Creating Item . . .');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item${page.url.search}`, {
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
			module.value.update(resp.items, resp.total_page);
			module.open(Dialogue, {
				message: 'Item Created',
				buttons: [
					{
						name: 'OK',
						icon: 'check',
						fn: () => {
							goto(`/${resp.item.slug}?edit=true`);
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

<Form
	title="Add New Item"
	description="Enter the item name to create a draft. You'll be taken to the item page to add details and images."
	error={error.error}
>
	<IG
		name="Name"
		icon="square-pen"
		error={error.name}
		placeholder="Name here"
		type="text"
		bind:value={form.name}
	/>

	<Button icon2="plus" onclick={validate}>Create Draft & Continue</Button>
</Form>
