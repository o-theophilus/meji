<script>
	import { Button } from '$lib/button';
	import { Content } from '$lib/layout';
	import { Log, Meta } from '$lib/macro';
	import { app, loading, notify } from '$lib/store.svelte.js';

	const submit = async () => {
		loading.open('Running maintenance...');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cron`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			notify.open('Maintenance complete');
		} else {
			error = resp;
		}
	};
</script>

<Log entity_type={'page'} />
<Meta title="Maintenance" />

<Content>
	<div class="page_title">Maintenance</div>

	<br />
	<Button onclick={submit} size="wide">Maintenance</Button>
</Content>

<style>
</style>
