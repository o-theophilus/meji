<script>
	import { goto } from '$app/navigation';
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { Note } from '$lib/info';
	import Status from './edit.svelte';

	let form = $state({});
	let error = $state({});

	const validate = async () => {
		error = {};

		if (!form.password) {
			error.password = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open('Deleting Blog . . .');
		let result = await fetch(`${import.meta.env.VITE_BACKEND}/blogs/${module.value.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		result = await result.json();
		loading.close();

		if (result.status == 200) {
			module.close();
			notify.open('Blog Deleted');
			goto('/blog');
		} else {
			error = result;
		}
	};
</script>

<Form title="Delete" error={error.error}>
	<Note status="400" note="Are you sure you want to delete this blog"></Note>

	<IG
		name="Password"
		icon="key-round"
		error={error.password}
		bind:value={form.password}
		type="password+"
		placeholder="Password here"
	></IG>

	<div class="line">
		<Button icon="arrow-left" onclick={() => module.open(Status, { ...module.value })}>Back</Button>
		<Button --button-background-color-hover="red" icon="trash-2" onclick={validate}>Delete</Button>
	</div>
</Form>
