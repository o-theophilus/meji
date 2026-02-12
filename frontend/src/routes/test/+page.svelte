<script>
	import Pagination from '$lib/input/pagination.svelte';
	import { Content } from '$lib/layout';

	let show_password = $state();
</script>

<Content>
	<!-- <Group name="hello 1" error="hello" type="text" icon="heart" placeholder="hello"></Group> -->
	<!-- <Group name="hello 2" type="textarea" placeholder="hello"></Group> -->
	<!-- <Group name="hello 3" type="code" placeholder="hello"></Group> -->
	<!-- <Group name="hello 4" value="6" type="number"></Group> -->

	<Pagination value="3" total_page="5"></Pagination>
	<!-- <Group name="hello 5" type="rating" placeholder="hello"></Group> -->
	<!-- <Group name="hello 6" type="date" placeholder="hello"></Group> -->
	<!-- <Group name="hello 7" bind:show_password type="password" placeholder="password"></Group> -->
	<!-- <Group name="hello 8" bind:show_password type="password++" placeholder="password"></Group> -->

	<!-- <Input --input-margin-top="16px" type="text" icon="heart" placeholder="hello"></Input> -->
	<!-- <Input --input-margin-top="16px" type="textarea" placeholder="hello"></Input> -->
	<!-- <Input --input-margin-top="16px" type="code" placeholder="hello"></Input> -->
	<!-- <Input --input-margin-top="16px" type="number" placeholder="hello"></Input> -->
	<!-- <Input --input-margin-top="16px" type="rating" placeholder="hello"></Input> -->
	<!-- <Input --input-margin-top="16px" type="date" placeholder="hello"></Input> -->
	<!-- <Input --input-margin-top="16px" type="password" placeholder="password"></Input> -->
	<!-- <Input --input-margin-top="16px" type="password++" placeholder="password"></Input> -->
</Content>
